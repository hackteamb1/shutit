'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function enterById() {
    var id_number = document.querySelector('#id_number').value;
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

var Passenger = function (_React$Component) {
    _inherits(Passenger, _React$Component);

    function Passenger(props) {
        _classCallCheck(this, Passenger);

        var _this = _possibleConstructorReturn(this, (Passenger.__proto__ || Object.getPrototypeOf(Passenger)).call(this, props));

        _this.removePassenger = _this.removePassenger.bind(_this);
        return _this;
    }

    _createClass(Passenger, [{
        key: 'removePassenger',
        value: function removePassenger() {
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
    }, {
        key: 'render',
        value: function render() {
            return React.createElement(
                'div',
                { className: 'passenger' },
                React.createElement(
                    'button',
                    { className: 'button button-remove', onClick: this.removePassenger },
                    'Remove'
                ),
                React.createElement(
                    'div',
                    { className: 'passenger-details' },
                    React.createElement(
                        'p',
                        null,
                        this.props.first_name,
                        ' ',
                        this.props.last_name
                    )
                )
            );
        }
    }]);

    return Passenger;
}(React.Component);

var PassengerFetcher = function (_React$Component2) {
    _inherits(PassengerFetcher, _React$Component2);

    function PassengerFetcher(props) {
        _classCallCheck(this, PassengerFetcher);

        var _this2 = _possibleConstructorReturn(this, (PassengerFetcher.__proto__ || Object.getPrototypeOf(PassengerFetcher)).call(this, props));

        _this2.state = { rendered: null };
        setInterval(function () {
            _this2.fetchPassengers();
        }, 1000);
        return _this2;
    }

    _createClass(PassengerFetcher, [{
        key: 'fetchPassengers',
        value: function fetchPassengers() {
            var _this3 = this;

            fetch('/api/state/10').then(function (response) {
                return response.json().then(function (json) {
                    var passengers = json.map(function (passenger) {
                        return React.createElement(Passenger, { first_name: passenger.first_name,
                            last_name: passenger.last_name,
                            number_in_queue: passenger.number_in_queue,
                            key: passenger.number_in_queue });
                    });
                    return React.createElement(
                        'div',
                        null,
                        passengers
                    );
                });
            }).then(function (fetched) {
                _this3.setState({ rendered: fetched });
            });
        }
    }, {
        key: 'render',
        value: function render() {
            return this.state.rendered;
        }
    }]);

    return PassengerFetcher;
}(React.Component);

ReactDOM.render(React.createElement(PassengerFetcher, null), document.getElementById('passengers'));
