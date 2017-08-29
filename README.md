# Exercise Catalog

The Exercise Catalog provides a simple website to manage your favorite exercise
instructional videos from YouTube. User's can login with Google or Facebook and
add, remove, or delete their own videos. In addition, user's can view all the
other existing videos on the site. Finally, JSON requests are provided for certain
views (more details are provided below).

Thanks to the good folks at Udacity for awesome instruction and support in
creating this project.

## Required Setup

Ready to get the website up and running? Let's set it up and get going!

1. <a href="https://www.virtualbox.org/wiki/Downloads">Virtual Box (download here)</a>
    - "VirtualBox is a general-purpose full virtualizer for x86 hardware, targeted
    at server, desktop and embedded use."
    - Translation: Think virtual computer.
    VirtualBox gives you a virtual computer you can play with, break, and rebuild
    without damaging your actual computer. Nifty! :bowtie:
    - Instructions: Simply install the correct platform package for your Operating
    System. Once installed, you don't even need to open it.

2. <a href="https://www.vagrantup.com/downloads.html">Vagrant (download here)</a>
    - "Vagrant
    is a tool for building and managing virtual machine environments in a single
    workflow."
    - Translation: Think helper for VirtualBox.
    - Instructions: Simply install the correct version for your Operating System.
    - Warning for Windows users: The Installer may ask you to grant network
    permissions to Vagrant or make a firewall exception. Be sure to allow this.
    - Verify: To verify the installation setup, open your Terminal and type
    `vagrant --version`. If successful, you will see your Vagrant version.

3. <a href="https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip">FSND-Virtual-Machine (download here)</a>
    - What? You don't know how to setup VirtualBox and Vagrant? No worries,
    the good folks at Udacity have created one for you! Sweet!
    - Even if you already know how to use VirtualBox and Vagrant, you still need
    to download and use this Vagrant build. It is preconfigured with necessary
    applications, plugins, and databases required for this tool.
    - Instructions:
        1) Unzip the folder and (optionally) move it into the directory
    you want it to live in (I use Documents).
        2) Use the terminal to cd into the directory `cd Documents/FSND-Virtual-Machine`
        3) Run the command `vagrant up` to start your Virtual Machine.
        4) Wait for a while :) -- this will take some time since it is installing
        an entire computer on your computer. Think about that! (\**mind explodes**)
        5) Once completed, your shell will return the prompt you are used to
        seeing. From here, you can log in to your new computer by typing
        `vagrant ssh` into the shell.
        6) Run the command `cd /vagrant`

4. <a href="https://github.com/lbuthman/udacity-catalog">Exercise Catalog Repo</a>
    - Here is the project repository hosted on GitHub. Feel free to Fork, Clone,
    Download, or ... Copy/Paste if you are a sadist.
    - Make sure to place the directory in your vagrant directory.

5. Populate the Database
    - In the terminal, cd into the project directory from Step 4 above.
    - Run `python3 database_setup.py`
    - Run `python3 lotsofexercises.py`

6. Start the WebApp and Try it Out!
    - In the terminal, make sure you are still in the project directory.
    - Run `python3 project.py`
    - Finally, in your browser, type `http://localhost:8000` and hit Enter.
    - That is it! Good Work :)

## Navigating the Website

Now it's time to have some fun!

You don't have to be logged in to see everything, but you do need to be logged
in to add, edit or delete exercises. Do keep in mind that you can only edit and
delete exercises that you have created. To signin, you will need a <a href="https://www.facebook.com/r.php">Facebook</a> or <a href="https://accounts.google.com/SignUp?hl=en">Google account</a>. If you don't
have one already, don't worry, they are easy to sign up for. Just click on their
links and follow the steps.

## Adding Exercises to the Catalog

While it is pretty easy to add exercises to a category in the catalog, there is
one gotcha I would like to point out. Here are the steps to follow when adding
a new item.

1. Navigate to the category you want to add an exercise to.
2. Scroll to the bottom of the page and click on the Add Icon.
3. Enter the data requested in the form.
4. For the YouTube URL, be sure to add the embedded link. You can find this
link when on the YouTube video. Find the 'Share' on the page, just under the
video title. After clicking on Share, find and click on Embed. You will then
look for src="https://www.youtube.com/embed/...". Copy everything inside those
quotes and use that for the YouTube URL.

## JSON Requests

Sometimes in life, you just got to get your JSON On. AmIRight?! Luckily, we
have provided several JSON endpoints for you to use at your pleasure.

1. /categories/JSON/
    -> this will return all the exercise categories and their data
2. /exercises/JSON/
    -> this will return all the exercises and their data
3. /<category-name>/exercises/JSON/
    -> this will return data for all the exercises of a specified category
    -> replace <category-name> with the category of your choice
4. /<category-name>/<exercise-name>/JSON/
    -> this will return one the data for a specific exercise
    -> replace <category-name> with the category of your choice and
    <exercise-name> with the exercise of your choice
