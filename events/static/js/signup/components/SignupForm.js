import React, {Component, Fragment} from 'react';
import Typography from "@material-ui/core/es/Typography/Typography";
import Button from "@material-ui/core/es/Button/Button";
import Grid from "@material-ui/core/es/Grid/Grid";
import axios from 'axios';
import Cookie from 'js-cookie';
import forEach from 'lodash/forEach';
import isEmpty from 'lodash/isEmpty';
import find from 'lodash/find';
import mapValues from 'lodash/mapValues';
import {updateParticipant} from '../actions';
import {Elements, StripeProvider} from 'react-stripe-elements';

import Question from "./Question";
import Stripe from "./Stripe";

class SignupForm extends Component {
  constructor(props) {
    super(props);

    let answers = {};

    props.event.signup_questions.forEach(({id, type}) => {
      if (type === 'multiple_choice') {
        answers[id] = []
      } else {
        answers[id] = ''
      }
    });

    this.state = {
      payed: props.feePayed,
      errors: {},
      answers
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    // this.handleStripeToken = this.handleStripeToken.bind(this);
    this.validate = this.validate.bind(this);
  }

  handleChange(id, value) {

    this.setState(prevState => ({
      answers: {
        ...prevState.answers,
        [id]: value
      }
    }));
  }

  handleSubmit() {
    const errors = this.validate();
    const {signupUrl, dispatcher} = this.props;

    const answers = mapValues(this.state.answers, answer => Array.isArray(answer) ? answer.join(',') : answer);

    this.setState({
      errors
    });

    if (isEmpty(errors)) {
      axios.post(signupUrl, {answers}, {
        headers: {
          "X-CSRFToken": Cookie.get('csrftoken')
        }
      }).then(response => {
            dispatcher(updateParticipant(response.data.participant));
          }
      )
    }
  }

  // handleStripeToken(token, error_callback) {
  //   const {paymentUrl} = this.props;
	//
  //   axios.post(paymentUrl, {
  //     token: token['id']
  //   }, {
  //     headers: {
  //       "X-CSRFToken": Cookie.get('csrftoken')
  //     }
  //   }).then(response => {
	// 		if (response['error']) {
	// 			console.log(response['error']);
	// 			//error_callback(errors);
	// 		}
  //     const errors = {...this.state, payed: true};
  //     this.setState({
  //       errors,
  //       payed: true
  //     });
  //   });
  // }

  validate() {
		const {answers, payed}=this.state;
    const {signup_questions, fee} = this.props.event;
    let errors = {};

    // if (fee > 0 && !payed) {
    //   errors['payment'] = true;
    // }

    forEach(answers, (answer, id) => {
      const question = find(signup_questions, {id: parseInt(id)});

      if (question.required && isEmpty(answer)) {
        errors[id] = true;
      }
    });

    return errors;
  }

	showErrors(errors) {
		this.setState({
			errors: errors
		})
	}

  render() {
    const {event, stripe_publishable, payment_url} = this.props;
    const {answers, errors, payed} = this.state;

    return (
        <Grid container spacing={16}>
          <Grid item>
            <Grid container spacing={16}>
              {event.fee > 0 && (
                  <Grid item sm={12}>
                    <Typography variant="caption" color={errors['payment'] && 'error'} gutterBottom>
                      Payment
                    </Typography>
                    <Typography>
                      {payed ? (
                          'The event fee has been paid!  🎉'
                      ) : (
                          <Fragment>
                            This event has a fee of {event.fee} SEK to sign up.

                            {event.open_for_signup && (
															<StripeProvider apiKey={this.props.stripe_publishable}>
															<Elements>
                                <Stripe
                                    //handleToken={this.handleStripeToken}
																		//createPaymentIntent={this.createPaymentIntent}
                                    stripe_publishable={stripe_publishable}
                                    // description={event.name}
                                    // amount={event.fee}
																		paymentUrl={this.props.paymentUrl}
																		handleSubmit={this.handleSubmit}
																		validator={this.validate}
																		showErrors={this.showErrors}
                                />
															</Elements>
															</StripeProvider>
                            )}
                          </Fragment>
                      )}
                    </Typography>
                  </Grid>
              )}
            </Grid>

            <Grid container spacing={16}>
              {event.signup_questions.map(question => <Question
                  key={question.id}
                  handleChange={this.handleChange}
                  value={answers[question.id]}
                  error={errors[question.id]}
                  {...question}/>)}
            </Grid>
          </Grid>
          <Grid item sm={12}>
            <Button
                disabled={!event.open_for_signup}
                onClick={this.handleSubmit}
                variant="contained"
                color="primary"
            >
              {event.open_for_signup ? "Sign Up" : "Not open for sign up"}
            </Button>
          </Grid>
        </Grid>
    )
  }
}

export default SignupForm;
