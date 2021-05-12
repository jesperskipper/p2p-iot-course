FROM amd64/node:10-alpine

# Install some extra packages to make sure we can build and "npm install" our dependencies later
# All is done in a single step to avoid unnecessarily building intermediate images

# Create app directory
WORKDIR /usr/src/app

# Copy package.json, package-lock.json and install app dependencies
# This is done before copying the actual app files to allow Docker to cache
# this stage and avoid reinstalling dependencies when only app files change
COPY package*.json ./

RUN npm install

# Our application listens on port 5000
EXPOSE 5000

# Bundle app source
COPY . .

# Start our application, this runs the "start" script defined in package.json
CMD [ "npm", "start" ]

# CMD [ "npm", "run", "starthttp" ]
