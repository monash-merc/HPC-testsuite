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
    # get a list of modules and exclude the header info
    modulelistp=subprocess.Popen("module -t avail 2>&1 | tail -n +13 | sed 's/(default)//'", shell=True, stdout=subprocess.PIPE)
    modulelist=modulelistp.communicate()[0].splitlines()
    # now we create a test for each module
    for module in modulelist:
        # first we get a list of what the module sets
        moduleshowp=subprocess.Popen("module show " + module + " 2>&1", shell=True, stdout=subprocess.PIPE)
        moduleshowlist=moduleshowp.communicate()[0].splitlines()
        # then we test that each line makes sense
        for moduleshowline in moduleshowlist:
            # this checks that if we define a path the path actually exists
            if moduleshowline.startswith("prepend-path"):
                moduletokenlist = moduleshowline.split(" ")
                #yes this needs to be made more sensible!
                for moduletoken in moduletokenlist:
                    # prepend-path always has the second to last token at the environment variable and then the dir
                    env_variable =  moduletokenlist[-3]
                    dir = moduletokenlist[-2]
                    # we need to treat compiler flags in a special way and drop the -I -L etc
                    if "FLAGS" in env_variable:
                         dir = moduletokenlist[-2][2:]
                         # also exclude flags that aren't paths
                         if not "/" in dir:
                             continue
                    test = test_dir_exists(dir)
                    setattr(TestSequense, "test_" + module + "_prepend-path_" + env_variable, test)                    
            
                    # if moduletoken.startswith("PATH"):
                        # dir = moduletokenlist[2] 
                        # test = test_dir_exists(dir)
                        # setattr(TestSequense, "test_" + module + "_prepend-path_PATH", test)
    unittest.main()
