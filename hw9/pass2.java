import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;


class GetPin {
    public static boolean checkPin(String pin) throws NoSuchAlgorithmException{
        byte[] pinBytes = pin.getBytes();
        for (int i = 0; i < 25; i++) {
            for (int j = 0; j < 400; j++) {
                MessageDigest md = MessageDigest.getInstance("MD5");
                md.update(pinBytes);
                byte[] digest = md.digest();
                pinBytes = (byte[]) digest.clone();
            }
        }
        String hexPinBytes = toHexString(pinBytes);
        return hexPinBytes.equals("d04988522ddfed3133cc24fb6924eae9");
    }

    public static String toHexString(byte[] bytes) {
        StringBuilder hexString = new StringBuilder();
        for (byte b : bytes) {
            String hex = Integer.toHexString(b & 255);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }

    public static void main(String[] args) throws NoSuchAlgorithmException{
        for (int i = 0; i < 1000000; i++) {
            String pin = String.format("%06d", i);
            if (checkPin(pin)) {
                System.out.println(pin);
            }
            if (i % 10000 == 0) {
                System.out.println(i);
            }
        }
    }
}
