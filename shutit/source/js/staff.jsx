function enterById() {
    let id_number = document.querySelector('#id_number').value;
    fetch('/api/state/enter_by_id/', {
           method: 'post',
           headers: new Headers({
                "X-CSRFToken": getCookie("csrftoken"),
                'Content-Type': 'application/json'
           }),
           body: JSON.stringify({
                 "passenger_id": id_number
           }),
           credentials: 'include'
    });

}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}


class Passenger extends React.Component {
    constructor(props) {
        super(props);
        this.removePassenger = this.removePassenger.bind(this);
    }

    removePassenger() {
        fetch('/api/state/remove_by_position/', {
	           method: 'post',
               headers: new Headers({
                    "X-CSRFToken": getCookie("csrftoken"),
		            'Content-Type': 'application/json'
	           }),
               body: JSON.stringify({
		             number_in_queue: this.props.number_in_queue
	           }),
               credentials: 'include'
        });
    }


    render() {
        return (
            <div className="passenger">
                <button className="button button-remove" onClick={this.removePassenger}>Remove</button>
                <div className="passenger-details">
                    <p>{this.props.first_name} {this.props.last_name}</p>
                </div>
            </div>
        );
    }
}

class PassengerFetcher extends React.Component {
    constructor(props) {
        super(props);
        this.state = {rendered: null};
        setInterval(() => {
            this.fetchPassengers();
        }, 2000);
    }

    fetchPassengers() {
        fetch('/api/state/10').then((response) => {
            return response.json().then((json) => {
                let passengers = json.map((passenger) =>
                    <Passenger first_name={passenger.first_name}
                                last_name={passenger.last_name}
                                number_in_queue={passenger.number_in_queue}
                             key={passenger.number_in_queue}/>
                );
                return <div>{passengers}</div>;
            });
        }).then((fetched) => {
            this.setState({ rendered: fetched });
        });
    };

    render() {
        return this.state.rendered;
    }
}


ReactDOM.render(
    <PassengerFetcher/>,
    document.getElementById('passengers')
);
