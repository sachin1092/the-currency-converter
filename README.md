Currency Converter Api
============

Currency Converter REST API
Data from:
[Bank of Canada](http://www.bankofcanada.ca) 


Usage
==========

**Base URL:** [https://the-currency-converter.herokuapp.com/](https://the-currency-converter.herokuapp.com/)

**Output:** JSON


REST operations
====================
	
###Get rates for all the currencies:
####GET `/currency/v1.0/`

###Get conversion rate for specific currencies: 
#### GET `currency/v1.0/<< from >>/<< to >>/` 
		
			Example.
			**U.S. dollar to Indian Rupee**
			"currency/v1.0/USD/INR/" 	 

Go to [https://the-currency-converter.herokuapp.com/](https://the-currency-converter.herokuapp.com/) for API Guide and Disclaimer

Feel free to send a pull request or fork. :)