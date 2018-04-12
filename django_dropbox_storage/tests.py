from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.test import TestCase
from django_dropbox_storage.storage import DropboxStorage


class DropboxStorageTest(TestCase):

    def setUp(self):
        self.location = '/django_storage_testing'
        self.storage = DropboxStorage(location=self.location)
        self.storage.base_url = '/test_media_url/'

    def tearDown(self):
        self.storage.delete(self.location)

    def test_no_access_token(self, *args):
        """
        Storage raises an exception if access token is empty.
        """
        with self.assertRaises(ImproperlyConfigured):
            DropboxStorage(token=None)
        with self.assertRaises(ImproperlyConfigured):
            DropboxStorage(token='')

    def test_file_access_options(self):
        """
        Standard file access options are available, and work as expected.
        """
        self.assertFalse(self.storage.exists('django_storage_test'))
        f = self.storage.open('django_storage_test', 'w')
        f.write('storage contents')
        f.close()
        self.assertTrue(self.storage.exists('django_storage_test'))

        f = self.storage.open('django_storage_test', 'r')
        self.assertEqual(f.read(), 'storage contents')
        f.close()

        self.storage.delete('django_storage_test')
        self.assertFalse(self.storage.exists('django_storage_test'))

    def test_exists_folder(self):
        """
        Storage creates a folder.
        """
        self.assertFalse(self.storage.exists('django_storage_test_exists'))
        self.storage.client.files_create_folder(self.location + '/django_storage_test_exists')
        self.assertTrue(self.storage.exists('django_storage_test_exists'))
        self.storage.delete('django_storage_test_exists')
        self.assertFalse(self.storage.exists('django_storage_test_exists'))

    def test_listdir(self):
        """
        Storage returns a tuple containing directories and files.
        """
        self.assertFalse(self.storage.exists('django_storage_test_1'))
        self.assertFalse(self.storage.exists('django_storage_test_2'))
        self.assertFalse(self.storage.exists('django_storage_dir_1'))

        f = self.storage.save('django_storage_test_1', ContentFile('custom content'))
        f = self.storage.save('django_storage_test_2', ContentFile('custom content'))
        self.storage.client.files_create_folder(self.location + '/django_storage_dir_1')

        dirs, files = self.storage.listdir(self.location)
        self.assertEqual(set(dirs), set([u'django_storage_dir_1']))
        self.assertEqual(set(files),
                         set([u'django_storage_test_1', u'django_storage_test_2']))

        self.storage.delete('django_storage_test_1')
        self.storage.delete('django_storage_test_2')
        self.storage.delete('django_storage_dir_1')

    def test_file_size(self):
        """
        Storage returns a url to access a given file from the Web.
        """
        self.assertFalse(self.storage.exists('django_storage_test_size'))
        f = self.storage.open('django_storage_test_size', 'w')
        f.write('these are 18 bytes')
        f.close()
        self.assertTrue(self.storage.exists('django_storage_test_size'))

        f = self.storage.open('django_storage_test_size', 'r')
        self.assertEqual(f.size, 18)
        f.close()

        self.storage.delete('django_storage_test_size')
        self.assertFalse(self.storage.exists('django_storage_test_size'))

    def test_file_delete(self):
        """
        Storage returns true if deletion was performed, false otherwise.
        """
        self.assertFalse(self.storage.exists('django_storage_test_delete'))
        f = self.storage.open('django_storage_test_delete', 'w')
        f.write('storage delete')
        f.close()
        self.assertTrue(self.storage.exists('django_storage_test_delete'))

        deleted = self.storage.delete('django_storage_test_delete')
        self.assertEqual(deleted, True)

        self.assertFalse(self.storage.exists('django_storage_test_delete'))

        deleted = self.storage.delete('django_storage_test_delete')
        self.assertEqual(deleted, False)
