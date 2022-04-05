from typing import Dict, Union

from db.models.page import Page


class PageSerializer:
    def __init__(self, page: Page, ordering: str = "unordered"):
        self.page = page
        self.ordering = ordering.lower()

    def get_page_results(self) -> Dict[str, int]:
        if self.ordering == "alphabetical":
            return self.page.get_results_ordered_by_alphabetical()

        if self.ordering == "frequency":
            return self.page.get_results_ordered_by_frequency()

        return self.page.results

    def retrieve_output(self) -> Dict[str, Union[str, Dict[str, int]]]:
        return {
            "target_url": self.page.target_url,
            "created at": self.page.created_at,
            "status": self.page.status,
            "results": self.get_page_results(),
        }
