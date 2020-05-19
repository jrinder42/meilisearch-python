from meilisearch.index import Index
from meilisearch.config import Config
from meilisearch.stat import Stat
from meilisearch._httprequests import HttpRequests

class Client():
    """
    A client for the MeiliSearch API

    A client instance is needed for every MeiliSearch API method to know the location of
    MeiliSearch and its permissions.
    """

    config = None

    health_path = "health"
    key_path = 'keys'
    sys_info_path = 'sys-info'
    version_path = 'version'

    def __init__(self, url, apiKey=None):
        """
        Parameters
        ----------
        url : str
            The url to the MeiliSearch API (ex: http://localhost:7700)
        apiKey : str
            The optional API key for MeiliSearch
        """
        self.config = Config(url, apiKey)

    def create_index(self, uid, primary_key=None, name=None):
        """Create an index.

        If the argument `uid` isn't passed in, it will be generated
        by MeiliSearch.

        Parameters
        ----------
        uid: str
            UID of the index
        primary_key: str, optional
            Attribute used as unique document identifier
        name: str, optional
            Name of the index
        Returns
        -------
        index : Index
            an instance of Index containing the information of the newly created index
        Raises
        ------
        HTTPError
            In case of any other error found here https://docs.meilisearch.com/references/#errors-status-code
        """
        index = Index(self.config, uid=uid)
        index.create(self.config, uid=uid, primary_key=primary_key, name=name)
        return index

    def get_indexes(self):
        """Get all indexes.

        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        Returns
        -------
        list
            List of indexes in dictionnary format. (e.g [{ 'uid': 'movies' 'primaryKey': 'objectID' }])
        """
        return Index.get_indexes(self.config)


    def get_index(self, uid):
        """Get an index.

        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        Returns
        -------
        index : Index
            an instance of Index containing the information of the index found
        """
        return Index.get_index(self.config, uid=uid)

    def get_all_stats(self):
        """Get statistics about indexes, database size and update date.

        Returns
        -------
        stats : dict
            Dictionnary with information about indexes, database size and update date.
        """
        return Stat.get_all_stats(self.config)

    def health(self):
        """Get health of meilisearch

        `204` http status response when meilisearch is healthy.

        Raises
        ----------
        HTTPError
            If meilisearch is not healthy
        """
        return HttpRequests.get(self.config, self.health_path)

    def update_health(self, health):
        """Update health of meilisearch

        Update health of meilisearch to true or false.

        Parameters
        ----------
        health: bool
            Boolean reprensenting the healthyness of meilisearch. True for healthy.
        """
        return HttpRequests.put(self.config, self.health_path, {'health': health})

    def get_keys(self):
        """Get all keys created

        Get list of all the keys that were created and all their related information.

        Returns
        ----------
        keys: list
            List of keys and their information.
            https://docs.meilisearch.com/references/keys.html#get-keys
        """
        return HttpRequests.get(self.config, self.key_path)

    def get_sys_info(self):
        """Get system information of meilisearch

        Get information about memory usage and processor usage.

        Returns
        ----------
        sys_info: dict
            Information about memory and processor usage.
        """
        return HttpRequests.get(self.config, self.sys_info_path)

    def get_version(self):
        """Get version meilisearch

        Returns
        ----------
        version: dict
            Information about version of meilisearch.
        """
        return HttpRequests.get(self.config, self.version_path)

    def version(self):
        """Alias for get_version

        Returns
        ----------
        version: dict
            Information about version of meilisearch.
        """
        return self.get_version()


