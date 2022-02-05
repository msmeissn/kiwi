from mock import patch
from pytest import (
    raises, fixture
)

from kiwi.defaults import Defaults
from kiwi.xml_state import XMLState
from kiwi.xml_description import XMLDescription
from kiwi.bootloader.config.systemd_spec_base import BootLoaderSystemdSpecBase


class TestBootLoaderSystemdSpecBase:
    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setup(self):
        Defaults.set_platform_name('x86_64')
        description = XMLDescription(
            '../data/example_config.xml'
        )
        self.state = XMLState(
            description.load()
        )
        self.bootloader = BootLoaderSystemdSpecBase(
            self.state, 'root_dir'
        )
        self.custom_args = {
            'boot_uuid': 'boot_uuid',
            'root_uuid': 'root_uuid',
            'kernel': 'kernel',
            'initrd': 'initrd',
            'boot_options': 'options'
        }

    @patch.object(BootLoaderSystemdSpecBase, 'setup_loader')
    @patch.object(BootLoaderSystemdSpecBase, 'set_loader_entry')
    def test_setup_disk_image_config(
        self, mock_setup_loader, mock_set_loader_entry
    ):
        self.bootloader.setup_disk_image_config(
            'boot_uuid', 'root_uuid', 'hypervisor',
            'kernel', 'initrd', 'options'
        )
        assert self.bootloader.custom_args == self.custom_args
        mock_setup_loader.assert_called_once_with('disk')
        mock_set_loader_entry.assert_called_once_with('disk')

    @patch.object(BootLoaderSystemdSpecBase, 'setup_loader')
    @patch.object(BootLoaderSystemdSpecBase, 'set_loader_entry')
    def test_setup_install_image_config(
        self, mock_setup_loader, mock_set_loader_entry
    ):
        self.bootloader.setup_install_image_config(
            'mbrid', 'hypervisor', 'kernel', 'initrd'
        )
        self.custom_args['mbrid'] = 'mbrid'
        assert self.bootloader.custom_args == self.custom_args
        mock_setup_loader.assert_called_once_with('install(iso)')
        mock_set_loader_entry.assert_called_once_with('install(iso)')

    @patch.object(BootLoaderSystemdSpecBase, 'setup_loader')
    @patch.object(BootLoaderSystemdSpecBase, 'set_loader_entry')
    def test_setup_live_image_config(
        self, mock_setup_loader, mock_set_loader_entry
    ):
        self.bootloader.setup_live_image_config(
            'mbrid', 'hypervisor', 'kernel', 'initrd'
        )
        self.custom_args['mbrid'] = 'mbrid'
        assert self.bootloader.custom_args == self.custom_args
        mock_setup_loader.assert_called_once_with('live(iso)')
        mock_set_loader_entry.assert_called_once_with('live(iso)')

    @patch.object(BootLoaderSystemdSpecBase, 'create_loader_image')
    def test_setup_disk_boot_images(self, mock_create_loader_image):
        self.bootloader.setup_disk_boot_images('uuid')
        self.custom_args['mbrid'] = 'mbrid'
        assert self.bootloader.custom_args == self.custom_args
        mock_create_loader_image.assert_called_once_with('disk')

    @patch.object(BootLoaderSystemdSpecBase, 'create_loader_image')
    def test_setup_install_boot_images(self, mock_create_loader_image):
        self.bootloader.setup_install_boot_images('mbrid')
        self.custom_args['mbrid'] = 'mbrid'
        assert self.bootloader.custom_args == self.custom_args
        mock_create_loader_image.assert_called_once_with('install(iso)')

    @patch.object(BootLoaderSystemdSpecBase, 'create_loader_image')
    def test_setup_live_boot_images(self, mock_create_loader_image):
        self.bootloader.setup_live_boot_images('mbrid')
        self.custom_args['mbrid'] = 'mbrid'
        assert self.bootloader.custom_args == self.custom_args
        mock_create_loader_image.assert_called_once_with('live(iso)')

    def test_setup_loader(self):
        with raises(NotImplementedError):
            self.bootloader.setup_loader('target')

    def test_set_loader_entry(self):
        with raises(NotImplementedError):
            self.bootloader.set_loader_entry('target')

    def test_create_loader_image(self):
        with raises(NotImplementedError):
            self.bootloader.create_loader_image('target')

    def test_write(self):
        # just pass
        self.bootloader.write()

    def test_setup_sysconfig_bootloader(self):
        # just pass
        self.bootloader.setup_sysconfig_bootloader()

    def test_write_meta_data(self):
        # just pass
        self.bootloader.write_meta_data()