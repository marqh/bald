import unittest

import h5py
import numpy as np

import bald
from bald.tests import BaldTestCase

def _fattrs(f):
    f.attrs['bald_._'] = 'http://binary-array-ld.net/experimental/'
    f.attrs['bald_._type'] = 'bald_._Container'
    return f

def _create_parent_child(f, pshape, cshape):
    dsetp = f.create_dataset("parent_dataset", pshape, dtype='i')
    dsetc = f.create_dataset("child_dataset", cshape, dtype='i')
    dsetp.attrs['bald_._type'] = 'bald_._Dataset'
    dsetp.attrs['bald_._reference'] = dsetc.ref
    dsetc.attrs['bald_._type'] = 'bald_._Dataset'
    return f


class Test(BaldTestCase):
        
    def test_valid_uri(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            f = _create_parent_child(f, (11, 17), (11, 17))
            f.close()
            self.assertTrue(bald.validate_hdf5(tfile))

    def test_invalid_uri(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            f = _create_parent_child(f, (11, 17), (11, 17))
            f.attrs['bald_._turtle'] = 'bald_._walnut'
            f.close()
            self.assertFalse(bald.validate_hdf5(tfile))

class TestArrayReference(BaldTestCase):
    def test_match(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            f = _create_parent_child(f, (11, 17), (11, 17))
            f.close()
            self.assertTrue(bald.validate_hdf5(tfile))

    def test_mismatch_zeroth(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            f = _create_parent_child(f, (11, 17), (11, 13))
            f.close()
            self.assertFalse(bald.validate_hdf5(tfile))

    def test_mismatch_oneth(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            f = _create_parent_child(f, (11, 17), (13, 17))
            f.close()
            self.assertFalse(bald.validate_hdf5(tfile))

    def test_match_plead_dim(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            # parent has leading dimension wrt child
            f = _create_parent_child(f, (4, 13, 17), (13, 17))
            f.close()
            self.assertTrue(bald.validate_hdf5(tfile))

    def test_match_clead_dim(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            # child has leading dimension wrt parent
            f = _create_parent_child(f, (13, 17), (7, 13, 17))
            f.close()
            self.assertTrue(bald.validate_hdf5(tfile))

    def test_mismatch_pdisjc_lead_dim(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            # child and parent have disjoint leading dimensions
            f = _create_parent_child(f, (4, 13, 17), (7, 13, 17))
            f.close()
            self.assertFalse(bald.validate_hdf5(tfile))

    def test_mismatch_pdisjc_trail_dim(self):
        with self.temp_filename('.hdf') as tfile:
            f = h5py.File(tfile, "w")
            f = _fattrs(f)
            # child and parent have disjoint trailing dimensions
            f = _create_parent_child(f, (13, 17, 2), (13, 17, 9))
            f.close()
            self.assertFalse(bald.validate_hdf5(tfile))



    # def test_match_(self):
    #      with self.temp_filename('.hdf') as tfile:
    #         f = h5py.File(tfile, "w")
    #         f = _fattrs(f)
    #         # 
    #         f = _create_parent_child(f, (), ())
    #         f.close()
    #         self.assert(bald.validate_hdf5(tfile))

if __name__ == '__main__':
    unittest.main()
