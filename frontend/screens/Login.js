import React, { Component } from 'react';
import { View, Text, StyleSheet, Image, KeyboardAvoidingView } from 'react-native';
import LoginForm from './LoginForm';

export default class Login extends Component {
    render() {
        return (
            <KeyboardAvoidingView behavior='padding' style={style.container}>
                <View style={style.logoContainer}>
                    <Image
                    style={style.logo}
                    source={require('../assets/logo.png')}
                    />
                    <Text style={style.title}>RockitChef</Text>
                </View>
                  <LoginForm />
            </KeyboardAvoidingView>
        );
    }
}

style = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ff793f',
  },
  title: {
    fontSize: 50,
    fontFamily: 'AlNile-Bold',
    textAlign: 'center',
    margin: 50,
    color: 'white',
  },
  logoContainer: {
      alignItems: 'center',
      flexGrow: 1,
      justifyContent: 'center',
  },
  logo: {
      width: 100,
      height: 100,
  },
});
