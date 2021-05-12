FROM arm32v7/node:10-buster-slim

# Install some extra packages to make sure we can build and "npm install" our dependencies later
# All is done in a single step to avoid unnecessarily building intermediate images
RUN apt-get update && apt-get install --no-install-recommends -y curl git gcc g++ make python2
RUN mkdir -p /usr/src && \
    curl -s http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz | tar -C /usr/src -xvz && \
    (cd /usr/src/bcm2835-1.60 && \
    ./configure --prefix=/usr && \
    make && \
    make install) && \
    git clone --branch V71 https://github.com/joan2937/pigpio.git /usr/src/pigpio && \
    (cd /usr/src/pigpio && \
    sed -i 's,/usr/local,/usr,' Makefile && \
    make && \
    make install) && \
    rm -rf /usr/src/{bcm2835-1.60,pigpio}

# Create app directory
WORKDIR /usr/src/app

# Copy package.json, package-lock.json and install app dependencies
# This is done before copying the actual app files to allow Docker to cache
# this stage and avoid reinstalling dependencies when only app files change
COPY package*.json ./

RUN npm install

# Our application listens on port 8080
# EXPOSE 8080

# Bundle app source
COPY . .

# Start our application, this runs the "start" script defined in package.json
CMD ["npm", "start" ]
