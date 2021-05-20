# coin game

Play the coin game and decide who gets the prize in restricted budget. 
All you need to do is modifying **wishlist.csv**

Coin game follows brownian motion and coin name becomes random seed of 
this stochastic process. Code of a brownian motion came from [Brownian motion with Python](https://towardsdatascience.com/brownian-motion-with-python-9083ebc46ff0)

---
## wishlist.csv
| name          | coin       | wishlist_won                     |
|---------------|------------|----------------------------------|
| player's name | coin name  | amount one wants from the budget | 

---
## requirements
```bash
$ pip install dash pandas
```
---
##  run
```bash
$ python coingame.py --total_budgets 1000000 --max_round 30
```

---
## example
![toy_example](example.gif)
