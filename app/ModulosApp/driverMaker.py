from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.firefox.service import Service
import sys


class MakeDriver:
	def __init__(self,Navegador):
		self.Navegador=Navegador.lower()


	def Create(self):
		self.driver = False
		if self.Navegador=="chrome":
		    #opciones de driver***************************************************************************************
		    options = webdriver.ChromeOptions()
		    options.add_experimental_option('excludeSwitches', ['enable-logging'])
		    chrome_options = webdriver.ChromeOptions()
		    prefs = {"profile.default_content_setting_values.notifications" : 2,'excludeSwitches':['enable-logging']}
		    chrome_options.add_experimental_option("prefs",prefs)
		    #opciones de driver***************************************************************************************
		    try:
		        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)                        
		    except:
		        self.driver = webdriver.Chrome(executable_path=tempdriver(r"C:\dchrome\chromedriver.exe"),chrome_options=chrome_options)

		elif self.Navegador=="edge":            
		    try:
		        self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
		    except Exception as e:
		        print("!",e)
		        self.driver = webdriver.Edge(r'C:\dchrome\msedgedriver.exe')
		        

		else:
		    if getattr(sys, 'frozen', False):
		        options = webdriver.FirefoxOptions()                
		        options.add_argument("--private")
		        try:
		            rutaDrivers=Service(r"C:\dchrome\geckodriver.exe")
		        except:
		            rutaDrivers = os.path.join(sys._MEIPASS, "./driver/geckodriver.exe")                
		    else:
		        rutaDrivers=Service(r"C:\dchrome\geckodriver.exe")
		        options = webdriver.FirefoxOptions()
		        options.add_argument("--private")
		    
		    self.driver = webdriver.Firefox(service=rutaDrivers ,options=options)


		if self.driver:
			return driver

#Driver = MakeDriver("Edge").Create()