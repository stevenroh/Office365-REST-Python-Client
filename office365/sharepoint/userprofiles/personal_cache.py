from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.base_entity import BaseEntity


class PersonalCache(BaseEntity):
    """Per user cache of key/value pairs organized by folders. Personal cache MAY be used for optimizing initial
    load performance of the protocol client, if obtaining initial set of data from personal cache is faster that
    requesting the data from the server."""

    def __init__(self, context):
        super(PersonalCache, self).__init__(context, ResourcePath("SP.UserProfiles.PersonalCache"))

    @property
    def cache_name(self):
        """
        :rtype: str or None
        """
        return self.properties.get("CacheName", None)

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.PersonalCache"
