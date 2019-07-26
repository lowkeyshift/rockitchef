import { connect } from "react-redux";
import Recommendations from "./Recommendations";
import { ADD_RECOMMENDATIONS } from "../redux/actions";

const mapStateToProps = state => {
  return {
    inventory_items: state.RecommendationReducer.inventory_items,
    recommendations: state.RecommendationReducer.recommendations
  };
};

const mapDispatchToProps = dispatch => {
  return {
    onAddRecommendations: recommendations => {
      dispatch(ADD_RECOMMENDATIONS(recommendations));
    }
  };
};

const VisibleRecommendations = connect(
  mapStateToProps,
  mapDispatchToProps
)(Recommendations);

export default VisibleRecommendations;
