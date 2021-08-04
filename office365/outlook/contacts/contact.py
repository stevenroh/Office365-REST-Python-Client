from office365.directory.extension import ExtensionCollection
from office365.directory.profilePhoto import ProfilePhoto
from office365.outlook.calendar.emailAddress import EmailAddress
from office365.outlook.mail.item import Item
from office365.outlook.mail.physical_address import PhysicalAddress
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.resource_path import ResourcePath


class Contact(Item):
    """User's contact."""

    @property
    def manager(self):
        """
        The name of the contact's manager.
        :rtype: str or None
        """
        return self.properties.get("manager", None)

    @manager.setter
    def manager(self, value):
        """
        Sets name of the contact's manager.
        :type value: str
        """
        self.set_property("manager", value)

    @property
    def mobile_phone(self):
        """
        The contact's mobile phone number.
        :rtype: str or None
        """
        return self.properties.get("mobilePhone", None)

    @mobile_phone.setter
    def mobile_phone(self, value):
        """
        Sets contact's mobile phone number.
        :type value: str
        """
        self.set_property("mobilePhone", value)

    @property
    def home_address(self):
        return self.get_property("homeAddress", PhysicalAddress())

    @property
    def email_addresses(self):
        """The contact's email addresses."""
        return self.get_property("emailAddresses", ClientValueCollection(EmailAddress))

    @email_addresses.setter
    def email_addresses(self, value):
        """Sets contact's email addresses."""
        self.set_property("emailAddresses", value)

    @property
    def extensions(self):
        """The collection of open extensions defined for the contact. Nullable."""
        return self.get_property('extensions',
                                 ExtensionCollection(self.context, ResourcePath("extensions", self.resource_path)))

    @property
    def photo(self):
        """Optional contact picture. You can get or set a photo for a contact."""
        return self.get_property('photo',
                                 ProfilePhoto(self.context, ResourcePath("photo", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "emailAddresses": self.email_addresses,
            }
            default_value = property_mapping.get(name, None)
        return super(Contact, self).get_property(name, default_value)
