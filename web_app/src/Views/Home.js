import React, { Component } from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import APIClient from '../apiClient';

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyles = makeStyles(theme => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

function SignIn(props) {
  const classes = useStyles();

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          theBridge
        </Typography>
        <form className={classes.form} onSubmit = {props.onSubmit} noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="startSong"
            label="Start Song"
            name="startSong"
            autoFocus
            onChange = {props.startSong}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="endSong"
            label="End Song"
            id="endSong"
            onChange = {props.endSong}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Generate Playlist
          </Button>
          <Grid container>
            <Grid item xs>
              <Link href="#" variant="body2">
                Confused on spotify URIs?
              </Link>
            </Grid>
            <Grid item>
              <Link href="#" variant="body2">
                {"Don't have an account? Sign Up"}
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
      <Box mt={8}>
        <Copyright />
      </Box>
    </Container>
  );
}

export default class Home extends Component{
  constructor(props){
    super(props)
    this.state = {
      startSong: '',
      endSong: '',
      trackList: [],
      isSubmitted: false
    };
    this.yoter= <p> yeet </p>
    this.handleSubmit = async event => {
      event.preventDefault()
      // var data = JSON.stringify(this.state)
      var data = this.state
      var apiClient = new APIClient();
      var res = await apiClient.createKudo(data)
      this.state.trackList = res

      this.setState({isSubmitted:true})
      console.log(res)
    }
    this.handleStart = async event => {
      this.state.startSong = event.target.value
      console.log(event.target.value)
    }
    this.handleEnd = async event => {
      this.state.endSong = event.target.value
    }
  }
  render(){
    return (
      <div className = "Home">
        <SignIn onSubmit = {this.handleSubmit} startSong = {this.handleStart}
        endSong = {this.handleEnd}/>
        {this.state.isSubmitted && <p> {this.state.trackList.toString()} </p>}
      </div>
    );
  }
}
// 53A0W3U0s8diEn9RhXQhVz, spotify:track:5hkdfA87RZvNaxl6XiveOA; 1UdQqCUR7RwB9YYJONwbdM, spotify:track:0K8Hm9Q7GbyucgQB5BhC5C
//   // <FormControlLabel
  //   control={<Checkbox value="remember" color="primary" />}
  //   label="Remember me"
  // />
