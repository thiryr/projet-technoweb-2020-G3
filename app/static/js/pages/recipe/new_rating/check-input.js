import current_rating from "./star-rating.js"

export function check_star_rating() {

    if (current_rating < 1 || current_rating > 5) {
        return false;
    }

    return true;

}