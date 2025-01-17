import os

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.internal.queries.upload_session import create_upload_session_query
from office365.sharepoint.base_entity_collection import BaseEntityCollection
from office365.sharepoint.files.file import File
from office365.sharepoint.files.creation_information import FileCreationInformation


class FileCollection(BaseEntityCollection):
    """Represents a collection of File resources."""

    def __init__(self, context, resource_path=None):
        super(FileCollection, self).__init__(context, File, resource_path)

    def upload(self, file_name, content):
        """Uploads a file into folder

        :type file_name: str
        :type content: bytes or str
        """
        return self.add(file_name, content, True)

    def create_upload_session(self, source_path, chunk_size, chunk_uploaded=None, **kwargs):
        """Upload a file as multiple chunks

        :param str source_path: path where file to upload resides
        :param int chunk_size: upload chunk size (in bytes)
        :param (long)->None or None chunk_uploaded: uploaded event
        :param kwargs: arguments to pass to chunk_uploaded function
        """
        file_size = os.path.getsize(source_path)
        if file_size > chunk_size:
            qry = create_upload_session_query(self, source_path, chunk_size, chunk_uploaded, **kwargs)
            self.context.add_query(qry)
            return qry.return_type
        else:
            with open(source_path, 'rb') as content_file:
                file_content = content_file.read()
            return self.add(os.path.basename(source_path), file_content, True)

    def add(self, url, content, overwrite=False):
        """
        Adds a file to the collection based on provided file creation information. A reference to the SP.File that
        was added is returned.

        :param str url: Specifies the URL of the file to be added. It MUST NOT be NULL. It MUST be a URL of relative
            or absolute form. Its length MUST be equal to or greater than 1.
        :param bool overwrite: Specifies whether to overwrite an existing file with the same name and in the same
            location as the one being added.
        :param str or bytes content: Specifies the binary content of the file to be added.
        """
        return_type = File(self.context)
        self.add_child(return_type)
        create_info = FileCreationInformation(url=url, overwrite=overwrite)
        qry = ServiceOperationQuery(self, "add", create_info.to_json(), content, None,  return_type)
        self.context.add_query(qry)
        return return_type

    def add_template_file(self, url_of_file, template_file_type):
        """Adds a ghosted file to an existing list or document library.

        :param int template_file_type: refer TemplateFileType enum
        :param str url_of_file: server relative url of a file
        """
        return_type = File(self.context)
        self.add_child(return_type)
        params = {
            "urlOfFile": url_of_file,
            "templateFileType": template_file_type
        }
        qry = ServiceOperationQuery(self, "addTemplateFile", params, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_url(self, url):
        """Retrieve File object by url"""
        return File(self.context, ServiceOperationPath("GetByUrl", [url], self.resource_path))

    def get_by_id(self, _id):
        """Gets the File with the specified ID."""
        return File(self.context, ServiceOperationPath("getById", [_id], self.resource_path))
