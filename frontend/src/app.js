class InfoTabPage extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			value: '',
			ingredients: ['happy','panda'],
			recommendations: ['url1','url2']
		}

		this.handleChange = this.handleChange.bind(this)
		this.produceIngredientElement = this.produceIngredientElement.bind(this)
		this.produceRecommendationElement = this.produceRecommendationElement.bind(this)
		this.produceIngredientElement = this.produceIngredientElement.bind(this)
		this.handleDeleteIngredientInstance = this.handleDeleteIngredientInstance.bind(this)
	
	}

	produceIngredientElement(ingredient,index) {
		return (
			<div>
			<li key={ingredient.id}>{ingredient}</li> 
			<button onClick={() => this.handleDeleteIngredientInstance(index)}> delete </button>
			</div>
			)
	}

	produceRecommendationElement(recommendation,index) {
		return (
			<div>
			<li key={recommendation.id}>{recommendation}</li>
			</div>
			)
	}

	handleDeleteIngredientInstance(index){
		this.setState((prevState) => {
			let newData = prevState.ingredients
			newData.splice(index,1)
			return {ingredients: newData}
		})
	}
	handleOnAdd(){
		const ingredient = this.state.value

		this.setState((prevState) => ({
					ingredients: prevState.ingredients.concat(ingredient)
				}))
	}

	handleChange(event) {
		this.setState({value: event.target.value})
	}
	render() {
		return (
		<div>
			<input type="text" value={this.state.value} onChange={this.handleChange} />
			<button onClick={() => this.handleOnAdd()}>Add to List</button>
			<ul>
				{this.state.ingredients.map((ingredient, index)=> this.produceIngredientElement(ingredient, index))}
			</ul>
			<button > Recommend me stuff </button>
			<ul>
				{this.state.recommendations.map((recommendation,index) => this.produceRecommendationElement(recommendation,index))}
			</ul>
		</div>
			)
	}
}

const template = <InfoTabPage />
const appRoot= document.getElementById('app')

ReactDOM.render(template, appRoot)