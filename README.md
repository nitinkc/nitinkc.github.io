# Restaurant Reservation 

GUI : Using HTML5, CSS3, Bootstrap Framework.

###Users: Customers and the Owner. Owner needs to be authenticated.

Customers | Creating a Reservation:

  1. Customers can reserve a table by providing date, time, party size, contact details.
  
      ***If reservation is in Waiting status, ask customer to confirm.
  2.  Provide a unique Confirmation Code and status back to the customer.

Customers | Edit/Cancel a Reservation:

1. Customers can edit an existing reservation using Confirmation Code.
2. Customers can edit date, time, and party size.

     ***Use same Confirmation Code and return new status.
3. Customers can cancel an existing reservation using Confirmation Code.

Owner | Login:

1. Owner can login using email and password.
2. No registration module is required.

Owner | View Reservation:

1. Owner can view list of reservations.
2. Click on each reservation item for more details.

Owner | View Seating Area

1. Owner can view seating area (tables) in a list form.
2. Each item can have ConfirmationCode, Size, Status, Since fields.
3. On clicking ConfirmationCode, open reservation detail screen.

Owner | Create and Edit a Reservation:

1. Same as Customer Create and Edit Reservation flows.

Owner | Profile & Settings:

1. Owner can view/edit restaurant profile details like Name, Contact, Email, Address etc.
2. Owner can update settings like Auto Assign, Restaurant Open/Closing days and times etc.

Owner | Assign Table:

1. Open reservation detail screen from list of reservations.
2. On clicking Assign Table, open seating map and select table.

Owner | Auto Assign Table:

1. If Auto Assign is enabled, system should assign the table to a new reservation automatically.

Owner | Change Table:

1. Owner should be able to change the table for a reservation.

Owner | View Contact List:

1. Owner can view contact list of all the customers and their past reservations.