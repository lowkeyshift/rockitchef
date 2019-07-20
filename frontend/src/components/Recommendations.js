import React, { Component } from 'react';
import { StyleSheet, FlatList, Text, View, Linking} from 'react-native';
import axios from 'axios';

import { ListItem, Card } from 'react-native-material-ui';
import { Icon } from 'react-native-elements';

/*
example recipe response:
{
        "id": 1,
        "chef": 1,
        "title": "testing",
        "recipe_url": "https://test429.com",
        "prep_time": "30 mins",
        "cook_time": "1 hr",
        "tags": [
            "sugar",
            "milk",
            "bacon",
            "salt"
        ],
        "ingredients": [
            {
                "id": 2,
                "item": "sugar",
                "quantity": "4 oz"
            },
            {
                "id": 1,
                "item": "cream cheese",
                "quantity": "10 oz"
            }
        ],
        "directions": [
            {
                "id": 1,
                "direction_text": ""
            }
        ]
    }
*/
class Recommendations extends Component {
    constructor(props) {

      super(props);
      this.state = {
        arrayHolder: [],
      }

    }

    componentDidMount() {
        axios
        .get(`recipes/recipes/`)
        .then(resp => {
            // TODO, add this to redux
            this.setState(prevState => ({
                arrayHolder: [...prevState.arrayHolder, ...resp.data.results]
            }))
        })
        
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

    clickItem(item) {
        Linking.openURL(item)
       }

    generateRightListElement = () => {
        return (<Icon
        name='rowing' />)
    }
    render() {
        return (
            <View style={styles.MainContainer}>
            <FlatList
                data={this.state.arrayHolder}
                width='100%'
                extraData={this.state.arrayHolder}
                keyExtractor={(item, index) => `list-${index}`}
                ItemSeparatorComponent={this.FlatListItemSeparator}
                renderItem={({item}) => 
                    <Card>
                        <ListItem
                            divider
                            centerElement={{
                            primaryText: `Make ${item.title} in ${item.cook_time}`,
                            }}
                            onPress={this.clickItem.bind(this, item.recipe_url)}
                            rightElement = {(<Icon name="rowing" />)}
                            // rightElement = {this.generateRightListElement.bind(this, item)}
                        />
                    </Card>
                }
            />
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

export default Recommendations;
