import sqlite3 as sql


def getCoins(userId: int) -> int:
  with sql.connect("economy.db") as con:

    cursor = con.cursor()
    cursor.execute("""SELECT Coins from ECONOMY WHERE userID = ? """, (userId,))
    data = cursor.fetchone()
    if data is None:
      cursor.execute("INSERT INTO ECONOMY (userID, Coins) VALUES (?,?)", (userId, 100))
      con.commit()
      return 100
    return data[0]

def removeMoney(userId: int, remove: int) -> bool | str:
  with sql.connect("economy.db") as con:
    cursor = con.cursor()

    current = getCoins(userId)
    if current is not None:
      cursor.execute("UPDATE ECONOMY SET Coins = current - ? WHERE userID = ?", (remove,userId))
      con.commit()
      return True, "Success!"
    else:
      return False, "Error: Can't remove coins!"

  

def addMoney(userId: int, add: int) -> bool | str:
  with sql.connect("economy.db") as con:

    cursor = con.cursor()
    current = getCoins(userid)
    if current is not None:
      cursor.execute("UPDATE ECONOMY SET Coins = current + ? WHERE userID = ?", (add, userId))
      con.commit()
      return True, "Success!"
    else:
      return False, "Error, Cant add coin!"
