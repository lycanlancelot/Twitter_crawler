import pymysql

def test_mysql():
	con = pymysql.connect(host='144.6.42.250',port=8080,user='root',passwd='123456',db='mydb')
	cur = con.cursor()


if __name__ == '__main__':
	test_mysql()