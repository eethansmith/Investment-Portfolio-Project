/* Basic Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #333; /* Dark background */
    color: #fff; /* Light text color for contrast */
    line-height: 1.6;
}

.container {
    max-width: 1100px;
    margin: auto;
    overflow: auto;
    padding: 0 20px;
}

#navbar {
    background: #444; /* Slightly lighter background for the navbar */
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
}

#navbar .logo {
    font-size: 30px;
    margin-left: 20px;
}

#navbar ul {
    list-style: none;
    display: flex;
}

#navbar ul li {
    padding: 0 20px;
}

#navbar ul li a {
    color: #fff;
    text-decoration: none;
    padding: 5px;
    transition: background-color 0.3s ease;
}

#navbar ul li a:hover {
    background-color: #555; /* Hover effect for links */
    border-radius: 5px;
}
