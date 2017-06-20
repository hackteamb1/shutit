
class Passenger extends React.Component {
    render() {
        return (
            <div className="passenger">
                <button className="button button-remove">Remove</button>
                <div className="passenger-details">
                    <p>{this.props.first_name} {this.props.last_name}</p>
                </div>
                <button className="button button-skip">Skip</button>
            </div>
        );
    }
}

class PassengerFetcher extends React.Component {
    constructor(props) {
        super(props);
        this.state = {rendered: null};
        this.fetchPassengers();
    }

    fetchPassengers() {
        fetch('/api/state/10').then((response) => {
            return response.json().then((json) => {
                let passengers = json.map((passenger) =>
                    <Passenger first_name={passenger.first_name}
                                last_name={passenger.last_name} key={passenger.number_in_queue}/>
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
