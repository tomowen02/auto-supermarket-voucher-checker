# auto-supermarket-voucher-checker

This project is designed to help a local charity which distributes supermarket food vouchers to families in need.

## Introduction
### The problem that the project aims to solve:
- The charity has long spreadsheets which contain information about beneficiaries and how much money has been given to them in the form of supermarket vouchers.
- The spreadsheets have a column stating the balances remaining on the vouchers. This reduces vouchers being dispensed to beneficiaries who are not redeeming them to avoid waste.
- Around 3-4 times per year, someone needs to manually work their way down the spreadsheets and click each url linking to a voucher so that they can check the balances and update the spreadsheets
- This process tends to take between 0.5 - 1.5 of a working day to complete per spreadsheet.
- This project automates the process by using web scraping to receive the data displayed by clicking on the links, and generating a new spreadsheet with the information gathered.


### For ASDA vouchers, the process of manually checking the balance is two-fold:
1. The link is clicked. This shows the user the 'voucher code' and 'pin'.
2. The user goes to ASDA's gift card balance checker. They input the voucher code and pin. At this point, they must also do a captcha to verify they're not a robot.
##### Unfortunately due to the captcha, I can only automate the first half of the process for ASDA vouchers.


### The process for manually checking the balances for other supermarkets only has one step:
The user clicks the link for the voucher, and the balance is displayed on the web page received
