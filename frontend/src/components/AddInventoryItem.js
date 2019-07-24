import React from "react";
import { connect } from "react-redux";
import {
  StyleSheet,
  FlatList,
  Text,
  View,
  Alert,
  TouchableOpacity,
  TextInput,
  Form,
  Input,
  Button
} from "react-native";
import { ADD_INVENTORY_ITEM } from "./redux/actions";

let AddInventoryItem = ({ dispatch }) => {
  let input = "Hello";
  return (
    <View>
      <Form
        onSubmit={e => {
          e.preventDefault();
          if (!input.value.trim()) {
            return;
          }
          console.log("hello");
          dispatch(ADD_INVENTORY_ITEM(input.value));
          input.value = "";
        }}
      >
        <Input
          ref={node => {
            input = node;
          }}
        />
        <Button type="submit">Add Ingredient</Button>
      </Form>
    </View>
    // <TextInput
    //          placeholder="Enter Value Here"
    //          onChangeText={data => this.setState({ textInput_Holder: data })}
    //          style={styles.textInputStyle}
    //          underlineColorAndroid='transparent'
    //          value={this.state.textInput_Holder}
    // />

    // <TouchableOpacity onPress={this.joinData} activeOpacity={0.7} style={styles.button} >

    //     <Text style={styles.buttonText}> Add Ingredients </Text>

    // </TouchableOpacity>
  );
};

AddInventoryItem = connect()(AddInventoryItem);

export default AddInventoryItem;
