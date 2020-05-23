from selenium import webdriver
import time

driver = webdriver.PhantomJS("C:\\Users\\Admin\\Desktop\\school_files\\Sem4\\Komplexe&Algoritme\\InsertTweets\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
sources = ["https://www.dailyfx.com/authors/"]
driver.get(sources[0]+"Paul_Robinson")
predicts = []

print(sources[0])