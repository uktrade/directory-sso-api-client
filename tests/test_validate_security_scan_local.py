from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from validate_security_scan_local import SIGNED_OFF_BY_TRAILER, main


class ValidateSecurityScanLocalTest(TestCase):
    def test_main_appends_signed_off_by_trailer(self):
        with TemporaryDirectory() as temp_dir:
            commit_msg_path = Path(temp_dir) / 'COMMIT_EDITMSG'
            commit_msg_path.write_text('Bump pytest\n', encoding='utf-8')

            with patch('sys.argv', ['validate_security_scan_local.py', str(commit_msg_path)]):
                result = main()

            assert result == 0
            assert commit_msg_path.read_text(encoding='utf-8') == f'Bump pytest\n\n{SIGNED_OFF_BY_TRAILER}\n'

    def test_main_replaces_existing_signed_off_by_trailer(self):
        with TemporaryDirectory() as temp_dir:
            commit_msg_path = Path(temp_dir) / 'COMMIT_EDITMSG'
            commit_msg_path.write_text(
                'Bump pytest\n\nSigned-off-by: Someone Else\n',
                encoding='utf-8',
            )

            with patch('sys.argv', ['validate_security_scan_local.py', str(commit_msg_path)]):
                result = main()

            assert result == 0
            assert commit_msg_path.read_text(encoding='utf-8') == f'Bump pytest\n\n{SIGNED_OFF_BY_TRAILER}\n'
