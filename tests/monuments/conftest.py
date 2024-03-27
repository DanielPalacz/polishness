import os
import tempfile

import pytest


@pytest.fixture
def t_file():
    """ Create a temporary file """

    db_fd, db_path = tempfile.mkstemp()

    yield db_path

    # close and remove the temporary file
    os.close(db_fd)
    os.unlink(db_path)
