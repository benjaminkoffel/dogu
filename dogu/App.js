import React from 'react';
import { StyleSheet, Text, View, Button, Platform, TouchableNativeFeedback, Animated, Easing } from 'react-native';
import { Camera, Permissions } from 'expo';

export default class App extends React.Component {
  
  constructor () {
    super()
    this.animatedValue = new Animated.Value(0)
  }

  state = {
    hasCameraPermission: null,
    mood: null
  };
  
  async componentWillMount() {
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({ hasCameraPermission: status === 'granted' });
  }

  onPressButton = async () => {
    if (this.camera) {
      let photo = await this.camera.takePictureAsync();
      var choices = ['H A P P Y R U', 'S A D R U', 'I N D E T E R M I N I B I R U'];
      this.setState(s => { 
        return { hasCameraPermission: s.hasCameraPermission, mood: choices[Math.floor(Math.random() * choices.length)] }
      });
      this.animatedValue.setValue(0);
      Animated.timing(
        this.animatedValue,
        {
          toValue: 1,
          duration: 8000,
          easing: Easing.linear
        }
      ).start();
    }
  };

  render() {
    const { hasCameraPermission, mood } = this.state;
    if (hasCameraPermission === true) {
      return (
        <View style={styles.container}>
          <Camera 
            style={styles.camera} 
            type={Camera.Constants.Type.back} 
            flashMode={Camera.Constants.FlashMode.on}
            ref={ref => {this.camera = ref;}}>
            <Animated.View
                style={{
                  opacity: this.animatedValue.interpolate({
                    inputRange: [0, 0.5, 1],
                    outputRange: [0, 1, 0]
                  }),
                  height: 1000,
                  backgroundColor: 'blue',
                  flex: 1,
                }}>
                <Text style={styles.displayText}>{mood}</Text>
              </Animated.View>
            <View
              style={styles.cameraContainer}>
              <TouchableNativeFeedback
                onPress={this.onPressButton}
                background={Platform.OS === 'android' ? TouchableNativeFeedback.SelectableBackground() : ''}>
                <View style={styles.button}>
                  <Text style={styles.buttonText}>what mood has my dogu?</Text>
                </View>
              </TouchableNativeFeedback>
            </View>
          </Camera>
        </View>
      );
    } else if (hasCameraPermission === false) {
      return (
        <View style={styles.button}>
          <Text style={styles.buttonText}>C A M E R A . I N A C C E S S I B I R U</Text>
        </View>
      );
    } else {
      return (
        <View />
      );
    }
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  camera: {
    flex: 1,
  },
  cameraContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'row',
  },
  button: {
    marginBottom: 60,
    width: 260,
    backgroundColor: '#2196F3',
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
  },
  buttonText: {
    padding: 20,
    color: 'white',
  },
  displayText: {
    padding: 40,
    fontSize: 40,
    fontWeight: 'bold',
    color: 'white',
  }
})
