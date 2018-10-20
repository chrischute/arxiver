import arxiv
import os
import re
import time


from urllib.request import urlretrieve


class ArXiver(object):
    """Class for getting papers from ArXiv."""
    def __init__(self, output_dir):
        self.paper_re = re.compile(r'https?://arxiv.org/(abs|pdf)/([0-9]+\.[0-9v]+)(\.pdf)?')
        self.output_dir = output_dir

    def get_paper(self, url):
        """Get a paper from ArXiv.

        Args:
            url: URL for paper.
        """
        id_match = self.paper_re.search(url)
        if id_match is None:
            raise RuntimeWarning('Could not find paper ID in URL: {}'.format(url))
        paper_id = id_match.group(2)
        papers = arxiv.query(id_list=[paper_id])
        if len(papers) == 0:
            raise RuntimeWarning('Query for ID {} returned zero papers'.format(paper_id))
        paper = papers[0]

        paper_dir = self._get_dir(paper_id)
        self._write_notes(paper, paper_id, paper_dir)
        self._write_pdf(paper, paper_id, paper_dir)

    def _get_dir(self, paper_id):
        """Get directory for saving a paper. Make the directory if it doesn't exist.

        Returns:
            paper_dir (string): Directory for saving paper PDF and notes.
        """
        paper_dir = os.path.join(self.output_dir, paper_id)
        os.makedirs(paper_dir, exist_ok=True)

        return paper_dir

    @staticmethod
    def _write_pdf(paper, paper_id, paper_dir):
        """Download and write PDF for a paper.

        Args:
            paper (obj): Paper object from `arxiv.download`.
            paper_dir (string): Directory for saving paper PDF and notes.
        """
        # Downloads file in obj (can be result or unique page) if it has a .pdf link
        if 'pdf_url' in paper and paper['pdf_url'] and 'title' in paper and paper['title']:
            # Get URL to download and path to save PDF
            download_url = paper['pdf_url'].replace('/arxiv.org/', '/export.arxiv.org/')
            print('Fetching from {}'.format(download_url))
            output_path = os.path.join(paper_dir, '{}.pdf'.format(paper_id))

            # Download PDF, limit rate to 1 per second
            download_start_time = time.time()
            urlretrieve(download_url, output_path)
            time_taken = time.time() - download_start_time
            if time_taken < 1:
                time.sleep(1. - time_taken)
        else:
            raise RuntimeError('Paper as no PDF URL or title: {}'.format(paper.paper_id))

    @staticmethod
    def _write_notes(paper, paper_id, paper_dir):
        """Write header notes for a paper in markdown format.

        Args:
            paper (obj): Paper object from `arxiv.download`.
            paper_dir (string): Directory for saving paper PDF and notes.
        """
        bullet_points = [('Title', paper.title_detail.value),
                         ('Authors', ', '.join(paper.authors)),
                         ('Year', str(paper.updated_parsed.tm_year)),
                         ('Link', paper.arxiv_url),
                         ('Abstract', paper.summary.replace('\n', ' '))]

        output_path = os.path.join(paper_dir, '{}.md'.format(paper_id))
        with open(output_path, 'w') as output_fh:
            output_fh.write('## Paper\n')
            for bullet_title, bullet_text in bullet_points:
                output_fh.write('  - **' + bullet_title + ':** ')
                output_fh.write(bullet_text + '\n')
