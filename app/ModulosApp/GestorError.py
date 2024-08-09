import sys


class ErrorHandle:
	def __init__(self,error):
		self.ERROR=error


	def ShowError(self):
		Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(self.ERROR).__name__, self.ERROR

		print("="*30,"Ignore error \n",Nomb_error,"\n",)

	def SaveError(self):
		pass