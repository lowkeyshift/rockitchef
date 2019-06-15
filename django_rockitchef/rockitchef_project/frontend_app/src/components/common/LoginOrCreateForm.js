import React, { Component } from 'react';
import { Button, View, Text, Image, TextInput, StyleSheet, KeyboardAvoidingView } from 'react-native';
import { Actions } from 'react-native-router-flux';
import axios from 'axios';


class LoginOrCreateForm extends Component {
  state = {
    username: '',
    password: '',
    firstName: '',
    lastName: '',
    email: '',
  }

  onUsernameChange(text) {
    this.setState({ username: text });
  }

  onPasswordChange(text) {
    this.setState({ password: text });
  }

  onFirstNameChange(text) {
    this.setState({ firstName: text });
  }

  onLastNameChange(text) {
    this.setState({ lastName: text });
  }

  onEmailChange(text) {
    this.setState({ email: text });
  }

  handleRequest() {
    const endpoint = this.props.create ? 'register' : 'login';
    const payload = { username: this.state.username, password: this.state.password }

    if (this.props.create) {
      payload.first_name = this.state.firstName;
      payload.last_name = this.state.lastName;
      payload.email = this.state.email;
    }

    axios
      .post(`/auth/${endpoint}/`, payload)
      .then(response => {
        const { token } = response.data;

        // We set the returned token as the default authorization header
        axios.defaults.headers.common.Authorization = `Token ${token}`;

        // Navigate to the home screen
        Actions.main();
      })
      .catch(error => console.log(error));
  }

  renderCreateForm() {
    const { fieldStyle, textInputStyle} = style;
    if (this.props.create) {
      return (
          <View style={fieldStyle}>
            <TextInput
              placeholder="First name"
              placeholderTextColor='rgba(255,255,255,0.7)'
              autoCorrect={false}
              onChangeText={this.onFirstNameChange.bind(this)}
              style={textInputStyle}
            />
            <TextInput
              placeholder="Last name"
              placeholderTextColor='rgba(255,255,255,0.7)'
              autoCorrect={false}
              onChangeText={this.onLastNameChange.bind(this)}
              style={textInputStyle}
            />
            <TextInput
              placeholder="Email"
              placeholderTextColor='rgba(255,255,255,0.7)'
              autoCorrect={false}
              onChangeText={this.onLastNameChange.bind(this)}
              keyboardType="email-address"
              autoCapitalize='none'
              autoCorrect={false}
              style={textInputStyle}
            />
          </View>
      );
    }
  }

  renderButton() {
    const buttonText = this.props.create ? 'Create' : 'Login';

    return (
      <Button title={buttonText} onPress={this.handleRequest.bind(this)}/>
    );
  }


  renderCreateLink() {
    if (!this.props.create) {
      const { accountCreateTextStyle } = style;
      return (
        <Text style={accountCreateTextStyle}>
          Or
          <Text style={{ color: 'blue' }} onPress={() => Actions.register()}>
            {' Sign-up'}
          </Text>
        </Text>
      );
    }
  }

  render() {
    const {
      formContainerStyle,
      fieldStyle,
      textInputStyle,
      buttonContainerStyle,
      accountCreateContainerStyle,
      container,
      logo,
      logoContainer,
      title
    } = style;

    return (
      <KeyboardAvoidingView behavior='padding' style={container}>
        <View style={formContainerStyle}>
        <View style={logoContainer}>
        <Image style={logo}
        source={require('../../../assets/logo.png')}
        />
        <Text style={title}>RockitChef</Text>
        </View>
          <View style={fieldStyle}>
          <TextInput
            placeholder="Username"
            placeholderTextColor='rgba(255,255,255,0.7)'
            returnKeyType='next'
            onSubmitEditing={() => this.passwordInput.focus()}
            onChangeText={this.onUsernameChange.bind(this)}
            keyboardType="email-address"
            autoCapitalize='none'
            autoCorrect={false}
            style={textInputStyle}

          />
          <TextInput
            placeholder="Password"
            autoCapitalize="none"
            placeholderTextColor='rgba(255,255,255,0.7)'
            autoCorrect={false}
            secureTextEntry
            returnKeyType='go'
            ref={(input) => this.passwordInput = input}
            onChangeText={this.onPasswordChange.bind(this)}
            style={textInputStyle}
         />
          </View>
          {this.renderCreateForm()}
        </View>
        <View style={buttonContainerStyle}>
          {this.renderButton()}
          <View style={accountCreateContainerStyle}>
            {this.renderCreateLink()}
          </View>
        </View>
      </KeyboardAvoidingView>
    );
  }
}


const style = StyleSheet.create({
container: {
  flex: 1,
  backgroundColor: '#ff793f',
},
    formContainerStyle: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  textInputStyle: {
      height: 40,
      backgroundColor: 'rgba(255,255,255,0.2)',
      marginBottom: 10,
      color: '#FFF',
      paddingHorizontal: 50,
  },
  buttonContainerStyle: {
    flex: 1,
    justifyContent: 'center',
    padding: 25
  },
  accountCreateTextStyle: {
    color: 'black'
  },
  accountCreateContainerStyle: {
    padding: 25,
    alignItems: 'center'
  },
  title: {
    fontSize: 40,
    fontFamily: 'AlNile-Bold',
    textAlign: 'center',
    margin: 50,
    color: 'white',
  },
  logo: {
      width: 100,
      height: 100,
  },
  logoContainer: {
      marginTop: 60,
      alignItems: 'center',
      flexGrow: 1,
      justifyContent: 'center',
  },
});


export default LoginOrCreateForm;
