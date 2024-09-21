# install uv
su ${_REMOTE_USER} << EOF
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH=$PATH:$HOME/.rye/bin' >> ~/.bashrc
EOF

# install cdk
su ${_REMOTE_USER} << EOF
npm install -g aws-cdk
EOF
