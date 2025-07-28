const express = require('express');
const mongoose = require('mongoose');

const app = express();
const port = 3000;

// MongoDB connection         password-and-host-and-user
mongoose.connect('mongodb://root:123@mongo-db:27017/mydb?authSource=admin', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => console.log('Connected to MongoDB'));

// Define a sample schema and model
const UserSchema = new mongoose.Schema({ name: String });
const User = mongoose.model('User', UserSchema);

// Route
app.get('/', async (req, res) => {
  const user = await User.create({ name: 'Luffy' });
  res.json({ message: 'User added!', user });
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
