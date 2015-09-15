# derived from http://stackoverflow.com/questions/32899/how-to-generate-dynamic-parametrized-unit-tests-in-python
import unittest
import subprocess
import os
 
class TestSequense(unittest.TestCase):
    pass

def test_generator(a, b):
    def test(self):
        self.assertEqual(a,b)
    return test

def test_dir_exists(dir):
    def test(self):
        self.assertTrue(os.path.isdir(dir),"ERROR: " + dir + " is not a directory")
    return test
 
if __name__ == '__main__':
    # dynamically create a test per module
    modulelistp=subprocess.Popen("module -t avail 2>&1 | tail -n +13 | sed 's/(default)//'", shell=True, stdout=subprocess.PIPE)
    modulelist=modulelistp.communicate()[0].splitlines()
    for module in modulelist:
        moduleshowp=subprocess.Popen("module show " + module + " 2>&1", shell=True, stdout=subprocess.PIPE)
        moduleshowlist=moduleshowp.communicate()[0].splitlines()
        for moduleshowline in moduleshowlist:
            if moduleshowline.startswith("prepend-path"):
                moduletokenlist = moduleshowline.split(" ")
                for moduletoken in moduletokenlist:
                    if moduletoken.startswith("PATH"):
                        dir = moduletokenlist[2] 
                        test = test_dir_exists(dir)
                        setattr(TestSequense, "test_" + module + "_prepend-path_PATH", test)
                    if moduletoken.startswith("LD_LIBRARY_PATH"):
                        dir = moduletokenlist[2]
                        test = test_dir_exists(dir)
                        setattr(TestSequense, "test_" + module + "_prepend-path_LD_LIBRARY_PATH", test)
                    if moduletoken.startswith("MANPATH"):
                        dir = moduletokenlist[2]
                        test = test_dir_exists(dir)
                        setattr(TestSequense, "test_" + module + "_prepend-path_MANPATH", test)

    unittest.main()
