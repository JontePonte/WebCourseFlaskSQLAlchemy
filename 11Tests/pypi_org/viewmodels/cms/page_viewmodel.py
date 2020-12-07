
import pypi_org.services.package_service as package_service
import pypi_org.services.cms_service as cms_service

from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class PageViewModel(ViewModelBase):
    def __init__(self, full_url: str):
        super().__init__()

        self.page = cms_service.get_page(full_url)
