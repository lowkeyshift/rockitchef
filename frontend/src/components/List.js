import React, { Component } from 'react';
import { StyleSheet, FlatList, Text, View, Alert, TouchableOpacity, TextInput } from 'react-native';
import { connect } from 'react-redux'
import Inventory from './InventoryItems'
import {ADD_INVENTORY_ITEM} from './redux/actions'

import AddInventoryItem from './AddInventoryItem'
class Inventory_List extends Component {
    constructor(props) {

      super(props);
      this.state = {
        textInput_Holder: ''
      }

    }

    componentDidMount() {
        // this.setState({ arrayHolder: [...this.array] })
    }

    joinData = () => {
        // redux
        this.props.onAddInventoryItem(this.state.textInput_Holder)
    }

      FlatListItemSeparator = () => {
          return (
            <View
              style={{
                height: 1,
                width: "100%",
                backgroundColor: "#607D8B",
              }}
            />
          );
        }

    GetItem(item) {

      Alert.alert(item);

    }

       render() {
           return (

             <View style={styles.MainContainer}>

               <TextInput
                 placeholder="Enter Value Here"
                 onChangeText={data => this.setState({ textInput_Holder: data })}
                 style={styles.textInputStyle}
                 underlineColorAndroid='transparent'
                 value={this.state.textInput_Holder}
               />

               <TouchableOpacity onPress={this.joinData} activeOpacity={0.7} style={styles.button} >

                 <Text style={styles.buttonText}> Add Ingredients </Text>

               </TouchableOpacity>
              {/* <AddInventoryItem /> */}
              <Inventory />
               {/* <FlatList
                 data={this.props.inventory_items}
                 width='100%'
                 extraData={this.props.inventory_items}
                 keyExtractor={(item, index) => `list-${index}`}
                 ItemSeparatorComponent={this.FlatListItemSeparator}
                 renderItem={({item}) => 
                    <Text style={styles.ingredient}
                          onPress={this.GetItem.bind(this, item.title)} > 
                      {item.title} 
                    </Text>}
               /> */}
               {/* <Text>Hellooo</Text> */}
             </View>

           );
         }
}

const styles = StyleSheet.create({

  MainContainer: {

    justifyContent: 'center',
    alignItems: 'center',
    flex: 1,
    margin: 2

  },

  ingredient: {
    padding: 10,
    fontSize: 18,
    height: 44,
  },

  textInputStyle: {

    textAlign: 'center',
    height: 40,
    width: '90%',
    borderWidth: 1,
    borderColor: '#4CAF50',
    borderRadius: 7,
    marginTop: 12
  },

  button: {

    width: '90%',
    height: 40,
    padding: 10,
    backgroundColor: '#4CAF50',
    borderRadius: 8,
    marginTop: 10
  },

  buttonText: {
    color: '#fff',
    textAlign: 'center',
  },

});

const mapDispatchToProps = dispatch => {
  return {
    onAddInventoryItem: itemName => {
      dispatch(ADD_INVENTORY_ITEM(itemName))
    }
  }
}

const List = connect(
  null,
  mapDispatchToProps
)(Inventory_List)
export default List;
