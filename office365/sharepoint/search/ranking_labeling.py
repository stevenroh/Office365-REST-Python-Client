from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.base_entity import BaseEntity


class RankingLabeling(BaseEntity):
    """Provides methods for getting and adding relevance judgments"""

    def __init__(self, context):
        static_path = ResourcePath("Microsoft.SharePoint.Client.Search.Query.RankingLabeling")
        super(RankingLabeling, self).__init__(context, static_path)

    def normalize_result_url(self, url):
        """
        A URL string after normalization. The input and output URL strings MUST resolve to the same document.

        :param str url: The URL for which the relevance judgment is added.
        """
        return_type = ClientResult(self.context)
        payload = {
            "url": url
        }
        qry = ServiceOperationQuery(self, "NormalizeResultUrl", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.RankingLabeling"
