import subprocess, os, glob, shutil

class TestRunner(object):
    """Builds a student's project; then runs unit tests on it.
    Grading is handled elsewhere, though - nota bene."""

    def __init__(self, config, assignment_dll, test_dll):
        super(TestRunner, self).__init__()

        self._mstest = '"' + config.mstest_path + '"'  # this is kind of yikes, but, sigh
        self._msbuild = '"' + config.msbuild_path + '"'

        self._assignment_dll = assignment_dll
        self._test_dll = test_dll

        self._test_string = self._mstest + ' "/testcontainer:"' + self._test_dll + ' "/detail:errormessage" >| out.txt'  # sorry; this sucks

    def RunTests(self, submission):
        print('Building project for submission: \t' + submission.submission_id)
        success = self.BuildStudentDLL(submission.directory)
        if not success: return False # getting a sweet zero

        success = self.PrepareStudentDLL(submission.directory, self._assignment_dll)
        if not success: return False

        os.chdir('./sandbox')
        if os.path.isfile('out.txt'):
            os.remove('out.txt')

        print('Running unit tests for submission: \t' + submission.submission_id)
        subprocess.Popen(self._test_string, stdout=subprocess.PIPE, shell=True)

        shutil.rmtree('./TestResults', ignore_errors=True)
        os.chdir('./..')

        print()
        return True

    def BuildStudentDLL(self, search_directory):
        results = glob.glob(search_directory + '/**/*.csproj', recursive=True)
       	
       	target = None
        if results: target = results[0]  # here's hoping that they have only one .sln

        if not target:
        	print('No .csproj found in ' + search_directory + '\n')
        	return False

        buildpath = self._msbuild + ' "' + target + '"'
        output = subprocess.Popen(buildpath, stdout=subprocess.PIPE, shell=True).stdout.read()

        output = str(output)
        # TODO this is a bit of a mess
        if '0 Errores' not in output:
        	print('Non-zero errors for directory: ' + search_directory + '\n')
        	return False

        return True

    def PrepareStudentDLL(self, search_directory, assignment, sandbox_dir='sandbox/'):
        goal_path = os.path.join(sandbox_dir, assignment)
        if os.path.isfile(goal_path):
            os.remove(goal_path)

        path = self.FindAssignmentDLLPath(search_directory, assignment)
        if not path:
        	print('No assignment dll of the appropriate name found after build: ' + search_directory)
        	return False # Maybe cheating?? # TODO add explanantions to everything
        os.rename(path, goal_path)
        return True

    def FindAssignmentDLLPath(self, directory, assignment_name):
        results = glob.glob(directory + '/**/Assignment1.dll', recursive=True)
        if results: return results[0]
        return None
