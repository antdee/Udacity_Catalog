# Furniture & More
This project is for a website where  registered users can list furniture and other home items for sale.
Users can navigate through the listings by room or by a seller's profile and find instructions on how to buy an item.
Registered users can also put up their own items for sale, by clicking 'Add Product' and completing the form.

## Getting Started
It is recommended to host the website server using a Virtual Machine.
1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/). Instructions on how to do so can be found on the websites.
2. Clone the [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm). There is a catalog folder provided for you, but no files have been included. If a catalog folder does not exist, simply create your own inside of the vagrant folder.
3. Copy the *Furniture & more* source code to the catalog folder.
4. Launch the Vagrant VM (by typing vagrant up in the directory fullstack/vagrant from the terminal). You can find further instructions on how to do so [here](https://www.udacity.com/wiki/ud088/vagrant).

## Deployment
You can run the server by running the ```project.py``` module.
It is set up to point at http://localhost:5000/ .
As an unregistered user, you will be able to browse all the listings, either by room or by seller profile. The ```buy``` button will take you to a page with the sellers email address where you can contact him and complete the transaction.
### Login
You can login using *Google* or *Facebook*. If it is your first time loging in, a new account with be created for you and stored in the database.
After that you will be able to post your own listings by clicking the [Add Product](http://localhost:5000/shop/new/) button.

### Thank you
