# Spend-Ez

Spend-Ez is a simple easy to use single-page dashboard for tracking expenses and maintaining a budget.

Try it out [**here**](http://ez.wilsonmacleod.com/spend-ez/login): 

**username**: ez_demo

**password:** demo123

Sign-up is currently disabled, I am considering implementing a sign-up, however for now please contact me through <website> if you would like your own account.
 
<gif> 

## Blurb

### Inspiration

I wanted to make a tool for my girlfriend and I to track and manage our expenses, hone my Flask skills and learn how to deploy a public facing web-applications.

This was driven by an urge to better understand where our money was going and to do so without having to use Mint or other programs that harvest data/use personal information.

### Implementation 

**Flask** over a **sqlite** database and **SQLAlchemy** for database communication. 

**Charts.js** for the live figures and a **Bootstrap** template for html and css.

Deployed using **Linode**, **Gunicorn**, **Nginx** and **Supervisord**. 

### Design choices

I wanted to keep the application as shallow and centralized as possible, a "one-stop-shop" where you can enter, visualized, track and compare your current and past spending habits. 

From one page you can update your budget, enter a new expense, view this and past months transactions, see your YTD spending and see which categories your spending mostly falls into.

### Feedback is welcomed and appreciate, please drop me a line here:
