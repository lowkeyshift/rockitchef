class InfoTabPage extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			value: '',
			ingredients: ['eggs','bacon','onion','sweet potato'],
			recommendations: []
		}

		this.handleChange = this.handleChange.bind(this)
		this.produceIngredientElement = this.produceIngredientElement.bind(this)
		this.produceRecommendationElement = this.produceRecommendationElement.bind(this)
		this.produceIngredientElement = this.produceIngredientElement.bind(this)
		this.handleDeleteIngredientInstance = this.handleDeleteIngredientInstance.bind(this)
		this.handleOnRecommendClick = this.handleOnRecommendClick.bind(this)
	}

	produceIngredientElement(ingredient,index) {
		return (
			<div key={ingredient.id}>
			<li key={ingredient.id}>{ingredient}</li> 
			<button onClick={() => this.handleDeleteIngredientInstance(index)} key={ingredient.id}> delete </button>
			</div>
			)
	}

	produceRecommendationElement(recommendation,index) {
		return (
			<div key={recommendation.id}>
			<li key={recommendation.id}>
				<a onClick={()=> window.open(recommendation)}> {recommendation }</a>
			</li>
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

	handleOnRecommendClick(){
		const recommendations = ['https://www.allrecipes.com/recipe/23224/microwave-pralines/']
		this.setState((prevState) => ({
					recommendations: [...prevState.recommendations,...recommendations]
				}))
	}

	render() {
		return (
		<div>
			<input type="text" value={this.state.value} onChange={this.handleChange} />
			<button onClick={() => this.handleOnAdd()}>Add to List</button>
			<ul>
				{this.state.ingredients.map((ingredient, index)=> this.produceIngredientElement(ingredient, index))}
			</ul>
			<button onClick={() => this.handleOnRecommendClick()}> Recommend me stuff </button>
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