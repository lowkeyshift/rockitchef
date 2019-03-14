'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var InfoTabPage = function (_React$Component) {
	_inherits(InfoTabPage, _React$Component);

	function InfoTabPage(props) {
		_classCallCheck(this, InfoTabPage);

		var _this = _possibleConstructorReturn(this, (InfoTabPage.__proto__ || Object.getPrototypeOf(InfoTabPage)).call(this, props));

		_this.state = {
			value: '',
			ingredients: ['happy', 'panda'],
			recommendations: ['url1', 'url2']
		};

		_this.handleChange = _this.handleChange.bind(_this);
		_this.produceIngredientElement = _this.produceIngredientElement.bind(_this);
		_this.produceRecommendationElement = _this.produceRecommendationElement.bind(_this);
		_this.produceIngredientElement = _this.produceIngredientElement.bind(_this);
		_this.handleDeleteIngredientInstance = _this.handleDeleteIngredientInstance.bind(_this);

		return _this;
	}

	_createClass(InfoTabPage, [{
		key: 'produceIngredientElement',
		value: function produceIngredientElement(ingredient, index) {
			var _this2 = this;

			return React.createElement(
				'div',
				null,
				React.createElement(
					'li',
					{ key: ingredient.id },
					ingredient
				),
				React.createElement(
					'button',
					{ onClick: function onClick() {
							return _this2.handleDeleteIngredientInstance(index);
						} },
					' delete '
				)
			);
		}
	}, {
		key: 'produceRecommendationElement',
		value: function produceRecommendationElement(recommendation, index) {
			return React.createElement(
				'div',
				null,
				React.createElement(
					'li',
					{ key: recommendation.id },
					recommendation
				)
			);
		}
	}, {
		key: 'handleDeleteIngredientInstance',
		value: function handleDeleteIngredientInstance(index) {
			this.setState(function (prevState) {
				var newData = prevState.ingredients;
				newData.splice(index, 1);
				return { ingredients: newData };
			});
		}
	}, {
		key: 'handleOnAdd',
		value: function handleOnAdd() {
			var ingredient = this.state.value;

			this.setState(function (prevState) {
				return {
					ingredients: prevState.ingredients.concat(ingredient)
				};
			});
		}
	}, {
		key: 'handleChange',
		value: function handleChange(event) {
			this.setState({ value: event.target.value });
		}
	}, {
		key: 'render',
		value: function render() {
			var _this3 = this;

			return React.createElement(
				'div',
				null,
				React.createElement('input', { type: 'text', value: this.state.value, onChange: this.handleChange }),
				React.createElement(
					'button',
					{ onClick: function onClick() {
							return _this3.handleOnAdd();
						} },
					'Add to List'
				),
				React.createElement(
					'ul',
					null,
					this.state.ingredients.map(function (ingredient, index) {
						return _this3.produceIngredientElement(ingredient, index);
					})
				),
				React.createElement(
					'button',
					null,
					' Recommend me stuff '
				),
				React.createElement(
					'ul',
					null,
					this.state.recommendations.map(function (recommendation, index) {
						return _this3.produceRecommendationElement(recommendation, index);
					})
				)
			);
		}
	}]);

	return InfoTabPage;
}(React.Component);

var template = React.createElement(InfoTabPage, null);
var appRoot = document.getElementById('app');

ReactDOM.render(template, appRoot);
