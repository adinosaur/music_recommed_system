#coding=utf8
import mysql.connector
import MySQLdb
from string import Template

class DBWriter:

	def __init__(self, database):
		self.db = mysql.connector.connect(
			user='root', passwd='12345', db=database, 
			host='127.0.0.1', charset="utf8",  use_unicode=True, raise_on_warnings=False
		)
		self.cursor = self.db.cursor()

class SearchPrompt(object):
	"""docstring for SearchPrompt"""
	
	def __init__(self):
		super(SearchPrompt, self).__init__()
		self.dbWriter = DBWriter(database='music_recommed_system_db')
		self.msgTemplate = Template("'%${msg}%'")

	def query(self, table, col, msg, topn):
		msg = self.msgTemplate.substitute(msg=msg)
		sql = """SELECT %s FROM %s WHERE %s LIKE %s LIMIT %d""" %(col, table, col, msg, topn)
		print sql
		self.dbWriter.cursor.execute(sql)
		return self.dbWriter.cursor.fetchall()

class SearchPromptList(object):
	
	def __init__(self):
		super(SearchPromptList, self).__init__()
		self.searchPrompt = SearchPrompt()
		self.l = list()
		self.l.append(("mymusic_singer", "name"))
		self.l.append(("mymusic_song", "title"))

	def query(self, msg, topn):
		resultList = list()
		for table, col in self.l:
			resultList.append(self.searchPrompt.query(table, col, msg, topn))
		return resultList

if __name__ == '__main__':
	searchPromptList = SearchPromptList()
	msg="一"
	topn = 10

	for l in searchPromptList.query(msg, topn):
		if l:
			for item in l:
				print item[1]
