import { connect } from "react-redux";
import Recommendations from "./Recommendations";
import { ADD_PROFILE } from "../redux/actions";

const mapStateToProps = state => {
  return {
    profile: state.ProfileReducer.profile
  };
};

const mapDispatchToProps = dispatch => {
  return {
    onAddRecommendations: recommendations => {
      dispatch(ADD_PROFILE(recommendations));
    }
  };
};

const VisibleRecommendations = connect(
  mapStateToProps,
  mapDispatchToProps
)(Recommendations);

export default VisibleRecommendations;
