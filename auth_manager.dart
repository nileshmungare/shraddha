import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '/auth/firebase_auth/firebase_user_provider.dart';
import 'base_auth_user_provider.dart';

abstract class AuthManager {
  Future signOut();
  Future deleteUser(BuildContext context);
  Future updateEmail({required String email, required BuildContext context});
  Future resetPassword({required String email, required BuildContext context});
  Future sendEmailVerification() async => currentUser?.sendEmailVerification();
  Future refreshUser() async => currentUser?.refreshUser();
}

mixin EmailSignInManager on AuthManager {
  Future<BaseAuthUser?> signInWithEmail(
      BuildContext context,
      String email,
      String password,
      );

  Future<BaseAuthUser?> createAccountWithEmail(
      BuildContext context,
      String email,
      String password,
      );
}

mixin PhoneSignInManager on AuthManager {
  Future<void> beginPhoneAuth({
    required BuildContext context,
    required String phoneNumber,
    required void Function(BuildContext) onCodeSent,
  });

  Future<BaseAuthUser?> verifySmsCode({
    required BuildContext context,
    required String smsCode,
  });
}

class FirebaseAuthManager extends AuthManager with PhoneSignInManager {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  String? _verificationId;

  @override
  Future<void> signOut() async {
    await _auth.signOut();
    debugPrint("User signed out.");
  }

  @override
  Future<void> deleteUser(BuildContext context) async {
    try {
      await _auth.currentUser?.delete();
      debugPrint("User deleted successfully.");
    } catch (e) {
      debugPrint("Delete user failed: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error deleting user: ${e.toString()}")),
      );
    }
  }

  @override
  Future updateEmail({required String email, required BuildContext context}) async {
    try {
      await _auth.currentUser?.updateEmail(email);
      debugPrint("Email updated successfully.");
    } catch (e) {
      debugPrint("Update email failed: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error updating email: ${e.toString()}")),
      );
    }
  }

  @override
  Future resetPassword({required String email, required BuildContext context}) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
      debugPrint("Password reset email sent.");
    } catch (e) {
      debugPrint("Reset password failed: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error resetting password: ${e.toString()}")),
      );
    }
  }

  @override
  Future<void> beginPhoneAuth({
    required BuildContext context,
    required String phoneNumber,
    required void Function(BuildContext) onCodeSent,
  }) async {
    try {
      await _auth.verifyPhoneNumber(
        phoneNumber: phoneNumber,
        verificationCompleted: (PhoneAuthCredential credential) async {
          await _auth.signInWithCredential(credential);
          debugPrint("Phone number automatically verified.");
        },
        verificationFailed: (FirebaseAuthException e) {
          debugPrint("Verification failed: ${e.message}");
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Phone verification failed: ${e.message}")),
          );
        },
        codeSent: (String verificationId, int? resendToken) {
          _verificationId = verificationId;
          onCodeSent(context);
          debugPrint("OTP Sent to $phoneNumber");
        },
        codeAutoRetrievalTimeout: (String verificationId) {
          _verificationId = verificationId;
        },
      );
    } catch (e) {
      debugPrint("Error in beginPhoneAuth: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error sending OTP: ${e.toString()}")),
      );
    }
  }

  @override
  Future<BaseAuthUser?> verifySmsCode({
    required BuildContext context,
    required String smsCode,
  }) async {
    try {
      PhoneAuthCredential credential = PhoneAuthProvider.credential(
        verificationId: _verificationId!,
        smsCode: smsCode,
      );

      UserCredential userCredential =
      await _auth.signInWithCredential(credential);

      debugPrint("Phone authentication successful. User: ${userCredential.user}");
      return FoodlyFirebaseUser(userCredential.user);
    } catch (e) {
      debugPrint("Error verifying SMS Code: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Invalid OTP. Please try again.")),
      );
      return null;
    }
  }
}
