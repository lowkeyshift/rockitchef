import { combineReducers } from "redux";
import { AuthReducer } from "./reducers/AuthReducer.js";
import { ProfileReducer } from "./reducers/ProfileReducer.js";
import { RecommendationReducer } from "./reducers/RecommendationReducer.js";
import { InventoryReducer } from "./reducers/InventoryReducer.js";

export default combineReducers({
  AuthReducer,
  ProfileReducer,
  RecommendationReducer,
  InventoryReducer
});
