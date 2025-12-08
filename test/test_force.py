# tests/test_test_force.py
import pytest
import numpy as np
import json
from src.primitives.force import Force, ForceStateDict

@pytest.fixture
def app(tmp_path):
    state_file = tmp_path / "state.json"
    app = StatefulApp(str(state_file))
    return app

def test_state_serialization(app):
    app.state = {'field_1': {'field_1': [1.0, 2.0], 'field_2': 42}}
    app.save()
    
    loaded = StatefulApp(str(app.state_file))
    assert loaded.state == app.state

@pytest.mark.parametrize("array_shape", [(3,), (2,2), (1,3,1)])
def test_numpy_roundtrip(app, array_shape):
    arr = np.random.rand(*array_shape)
    app.state['field_2'] = arr.tolist()
    app.save()
    
    loaded_arr = np.array(app.state['field_2'])
    np.testing.assert_array_equal(loaded_arr, arr)


